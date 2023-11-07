use axum::{
    extract::{FromRef, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use pyo3::prelude::*;
use pyo3::types::PyList;
use serde::{Deserialize, Serialize};
use std::fs;
use std::sync::Arc;
use tokio::{signal, task};

// Investigate exposing a "PyModel" rust struct
struct PyModel(Py<PyAny>);

#[derive(Clone)]
struct AppState {
    // that holds some api specific state
    model_call: Arc<PyModel>,
}

#[derive(Deserialize)]
struct InvocationRequest {}

#[derive(Serialize)]
struct InvocationResponse {}

fn init(model_path: &str) -> AppState {
    pyo3::prepare_freethreaded_python();
    let py_model = fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/example/example/predict.py"))
        .expect("Could not read predict.py");
    let module_path = concat!(env!("CARGO_MANIFEST_DIR"), "/example");

    let model_call: Py<PyAny> = Python::with_gil(|py| {
        // Add the example module to the path
        let syspath: &PyList = py.import("sys")?.getattr("path")?.downcast()?;
        syspath.insert(0, module_path)?;
        println!("Inserted module in path {}", module_path);

        let model: Py<PyAny> = PyModule::from_code(py, &py_model, "", "")?.into();
        println!("Loaded model module");

        // Load the model into global scope
        model.getattr(py, "load_model")?.call1(py, (model_path,))?;
        println!("Loaded model object");

        let model_call = model.getattr(py, "run_model")?;
        PyResult::Ok(model_call)
    })
    .unwrap();
    AppState {
        model_call: Arc::new(PyModel(model_call)),
    }
}

// basic handler that responds with a static string
async fn invoke(State(api_state): State<AppState>) -> &'static str {
    let val = task::spawn_blocking(move || {
        Python::with_gil(|py| api_state.model_call.0.call(py, (1, 2), None)).unwrap()
    })
    .await
    .unwrap();
    println!("rust invoked model {}", val);
    "Success"
}

#[tokio::main(flavor = "multi_thread")]
async fn main() {
    let state = init("model.pkl");

    // build our application with a route
    let app = Router::new()
        .route("/invoke", get(invoke))
        .with_state(state);

    // run our app with hyper, listening globally on port 3000
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    println!("signal received, starting graceful shutdown");
}

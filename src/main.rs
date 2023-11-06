use pyo3::prelude::*;
use std::sync::{Arc, Mutex, RwLock};
use std::thread;

fn main() -> PyResult<()> {
    pyo3::prepare_freethreaded_python();
    let py_model = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/example/model.py"));
    let model: Py<PyAny> = Python::with_gil(|py| {
        let model: Py<PyAny> = PyModule::from_code(py, py_model, "", "")?.into();
        PyResult::Ok(model)
    })?;
    let model = Arc::new(model);

    for j in 1..5 {
        let model = model.clone();
        thread::spawn(move || {
            Python::with_gil(|py| {
                for i in 1..10 {
                    let val = model.getattr(py, "run_model")?.call(py, (j, i), None)?;
                    println!("rthread:{} {}", j, val);
                }
                PyResult::Ok(())
            })
            .unwrap();
        });
    }

    Python::with_gil(|py| {
        for i in 1..10 {
            let val = model.getattr(py, "run_model")?.call(py, (0, i), None)?;
            println!("rthread:{} {}", 0, val);
        }
        PyResult::Ok(())
    })?;

    Ok(())
}

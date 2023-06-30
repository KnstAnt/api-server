#![allow(non_snake_case)]

use std::{collections::{HashMap, HashSet}};
use std::io::Write;
use std::process::{Command, Stdio};

use log::{debug, warn};
use rusqlite::{
    // Connection, Statement, 
    Error
};

type RowMap = HashMap<String, serde_json::Value>;
///
/// 
pub struct PythonQuery {
    path: String,
    params: String,
}

impl PythonQuery {
    ///
    pub fn new(path: &str, sql: String) -> PythonQuery {
        Self {
            path: path.into(),
            params: sql.to_string(),
        }
    }
    ///
    pub fn execute(&self) -> Result<Vec<RowMap>, String> {
        let path = self.path.clone();
        debug!("PythonQuery.execute | script: {:?}\n\twith params: {:?}", self.path, self.params);
        let program = "python3";
        debug!("PythonQuery.execute | executing command: {:?}", program);

        match Command::new(program)
                    .arg(path)
                    .stdin(Stdio::piped())
                    .stderr(Stdio::piped())
                    .stdout(Stdio::piped())
                    .spawn() {
            Ok(mut child) => {
                debug!("PythonQuery.execute | command child: {:?}", &child);
                debug!("PythonQuery.execute | sending stdin data...");
                child.stdin
                    .as_mut()
                    .ok_or("Child process stdin has not been captured!").unwrap()
                    .write_all(self.params.as_bytes()).unwrap();
                let output = child.wait_with_output().unwrap();
                debug!("PythonQuery.execute | command output: {:?}", output);
                let result = if output.status.success() {
                    let mut result: Vec<RowMap> = vec![];
                    let rawOutput = String::from_utf8(output.stdout).unwrap();
                    debug!("PythonQuery.execute | rawOutput: {:?}", rawOutput);
                    // let words = raw_output.split_whitespace()
                    //     .map(|s| s.to_lowercase())
                    //     .collect::<HashSet<_>>();
                    // debug!("PythonQuery.execute | Found {} unique words:", words.len());
                    // debug!("PythonQuery.execute | {:?}", words);
                    Ok(result)
                } else {
                    let err = String::from_utf8(output.stderr).unwrap();
                    warn!("PythonQuery.execute | python script error: {:?}", err);
                    Err(err)
                    // error_chain::bail!("External command failed:\n {}", err);
                };
                result
            },
            Err(err) => {
                warn!("PythonQuery.execute | python script error: {:?}", err);
                Err(err.to_string())
            },
        }
    }    
}
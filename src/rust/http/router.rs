use std::fs;

use super::server::{HttpRequest, HttpResponse, HttpStatusCode, HttpVerb, code_to_status};

const EMPTY_CONTENTS: &str = "";
const PATH_SEP: &str = "/";

const NOT_FOUND_PATH: &str = "serve/404.html";

// TODO generalize
const ROOT_SERVE: &str = "serve/chess.html";

fn resp_not_found() -> HttpResponse {
    HttpResponse {
        status: code_to_status(&HttpStatusCode::NotFound),
        body: fs::read_to_string(NOT_FOUND_PATH).unwrap_or(EMPTY_CONTENTS.to_owned())
    }
}

fn resp_5XX(code: &HttpStatusCode) -> HttpResponse {
    let path = format!("serve/{:?}.html", code);
    HttpResponse {
        status: code_to_status(code),
        body: fs::read_to_string(path).unwrap_or(EMPTY_CONTENTS.to_owned())
    }
}

fn srv_path_to_resp(file_path: &str) -> HttpResponse {
    fs::read_to_string(file_path)
        .map(|c| {
            HttpResponse {
                status: code_to_status(&HttpStatusCode::Ok),
                body: c
            }
        })
        .unwrap_or(resp_not_found())
}

// TODO generalize
pub fn route(request: HttpRequest) -> HttpResponse {
    println!("Incoming Request for {} {}", HttpVerb::to_str(&request.verb), request.path);

    match request.verb {
        HttpVerb::GET => {
            return if request.path == PATH_SEP {
                srv_path_to_resp(ROOT_SERVE)
            } else {
                let path_tokens: Vec<_> = request.path.split(PATH_SEP).collect();

                // TODO generalize
                if path_tokens.len() < 3 || path_tokens.len() > 4 {
                    resp_not_found()
                } else {
                    let mut vec = Vec::new();
                    vec.push("serve");
                    vec.push(path_tokens[2]);

                    if path_tokens.len() == 4 {
                        vec.push(path_tokens[3]);
                    }
                    srv_path_to_resp(&vec.join(PATH_SEP))
                }
            };
        }
        HttpVerb::POST => {
            return resp_5XX(&HttpStatusCode::NotImplemented);
        }
        HttpVerb::DELETE => {
            return resp_5XX(&HttpStatusCode::NotImplemented);
        }
        _ => return resp_5XX(&HttpStatusCode::NotImplemented)
    }
}
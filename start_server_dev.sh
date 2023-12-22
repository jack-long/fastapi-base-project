#!/bin/bash
cd $(git rev-parse --show-toplevel)/
export API_MODE=dev
uvicorn app.main:app --reload
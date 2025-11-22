CREATE TABLE request_source (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE data_request (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    status INTEGER NOT NULL,
    created_on TIMESTAMP NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    request_source_id VARCHAR(100) NOT NULL REFERENCES request_source(id)
);

-- Create index on status for filtering
CREATE INDEX idx_data_request_status ON data_request(status);

-- Create index on request_source_id for joins
CREATE INDEX idx_data_request_request_source_id ON data_request(request_source_id);

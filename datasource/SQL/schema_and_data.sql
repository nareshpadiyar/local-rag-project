CREATE TABLE incidents (
  incident_id VARCHAR(20) PRIMARY KEY,
  severity VARCHAR(10),
  service VARCHAR(50),
  region VARCHAR(50),
  status VARCHAR(30),
  root_cause VARCHAR(200)
);

INSERT INTO incidents VALUES
('INC1001','Sev2','Compute','us-east-1','Resolved','Stale image-store queue'),
('INC1002','Sev1','Network','eu-west-1','Resolved','Border router software fault'),
('INC1003','Sev3','Compute','ap-south-1','Resolved','Capacity threshold');

-- Policy: production backup retention is 35 days.

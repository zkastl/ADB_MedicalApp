create clustered columnstore index idx on dbo.MOCK_PATIENT_RECORDS with (data_compression=columnstore_archive);
GO
create clustered index rowidx on dbo.MOCK_PATIENT_RECORDS (first_name, last_name);
GO
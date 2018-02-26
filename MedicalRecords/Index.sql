USE TestDatabase;
create nonclustered columnstore index c_idx on dbo.medical_records (id, first_name, last_name);
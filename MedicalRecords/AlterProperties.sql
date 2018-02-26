USE TestDatabase;
GO
-- Check the state of the snapshot_isolation_framework
-- in the database.
SELECT name, recovery_model,
     recovery_model_desc AS description
FROM sys.databases
WHERE name = N'TestDatabase';
GO
USE master;
GO
ALTER DATABASE TestDatabase
    SET RECOVERY SIMPLE;
GO
-- Check again.
SELECT name, recovery_model,
     recovery_model_desc AS description
FROM sys.databases
WHERE name = N'TestDatabase';
GO
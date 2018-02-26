using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
using System.IO;
using System.Diagnostics;

namespace MedicalRecords
{
    class Program
    {
        private const string connString = @"Data Source=(LocalDB)\MSSQLLocalDB;AttachDbFilename='C:\Users\zkast\AppData\Local\Microsoft\Microsoft SQL Server Local DB\Instances\MSSQLLocalDB\ADB_DB.mdf';Integrated Security=True;Connect Timeout=30";
        private const string selectionQuery = "select * from [dbo].[MOCK_PATIENT_RECORDS] where current_state='New York' order by last_name";
        private const string indexColumnQuery = "create nonclustered columnstore index c_idx on dbo.MOCK_PATIENT_RECORDS (id, first_name, last_name)";
        private const string propertyString = "";

        static void Main(string[] args)
        {
            /* Basic idea
            // 1. Create tables on database
            // 2. create index row and column
            // 3. Find some way to demonstrate this.
            */

            // Create connection objects
            SqlConnection conn = new SqlConnection(connString);

            SqlCommand cmd = new SqlCommand
            {
                Connection = conn
            };

            // Open connection and load database
            conn.Open();
            using (StreamReader sr = new StreamReader(new FileStream(@"1MillionRecords.sql", FileMode.Open)))
                cmd.CommandText = sr.ReadToEnd();
            cmd.ExecuteNonQuery();

            // Create objects for reading queries
            cmd.CommandText = selectionQuery;
            cmd.CommandTimeout = 0;
            SqlDataReader reader = ExecuteQueryWithTimer(cmd);

            // Read entries and write to log            
            using (StreamWriter sw = new StreamWriter(new FileStream(@"out.log", FileMode.Create)))
            {
                while (reader.Read())
                {
                    object[] row = new object[reader.FieldCount];
                    reader.GetValues(row);

                    foreach (object o in row)
                        sw.Write(o.ToString() + "  |  ");
                    sw.Write("\n");
                }
            }

            //Close the connection
            conn.Close();
        }

        private static SqlDataReader ExecuteQueryWithTimer(SqlCommand command)
        {
            Stopwatch sw = new Stopwatch();
            sw.Start();
            SqlDataReader reader = command.ExecuteReader();
            sw.Stop();
            Console.WriteLine("Ellapsed time (ms): " + sw.ElapsedMilliseconds + "ms");

            return reader;
        }
    }
}

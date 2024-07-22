using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace SuggestPlan
{
    class Program
    {
        static string PythonPath = @"C:\Users\asli\Desktop\suggest-payment-plans\venv\Scripts\python.exe";
        static string ScriptPath = @"C:\Users\asli\Desktop\suggest-payment-plans\run.py";

        static async Task<List<Dictionary<string, object>>> GetSelected()
        {
            var inputData = new
            {
                start_date_year = 1403,
                start_date_month = 8,
                start_date_day = 20,
                total = 100.0,
                cash_amount = 20.0,
                number_of_month = 3,
                check_number = 3,
                max_discount_percentage = 0.2,
                max_raas_days = 65,
                max_price_change = 3,
                number_of_generated_pricess = 100
            };
            string inputJson = JsonConvert.SerializeObject(inputData);
            ProcessStartInfo start = new ProcessStartInfo
            {
                FileName = PythonPath,
                Arguments = ScriptPath,
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };
            using (Process process = new Process { StartInfo = start })
            {
                process.Start();
                using (StreamWriter writer = process.StandardInput)
                {
                    await writer.WriteLineAsync(inputJson);
                }

                Task<string> outputTask = process.StandardOutput.ReadToEndAsync();
                Task<string> errorTask = process.StandardError.ReadToEndAsync();

                await Task.WhenAll(outputTask, errorTask);

                string outputJson = outputTask.Result;
                string error = errorTask.Result;

                if (!string.IsNullOrEmpty(error))
                {
                    throw new Exception($"Error from Python script: {error}");
                }
                int startIndex = outputJson.IndexOf('[');
                if (startIndex >= 0)
                {
                    outputJson = outputJson.Substring(startIndex);
                }

                var outputData = JsonConvert.DeserializeObject<List<Dictionary<string, object>>>(outputJson);
                return outputData;
            }
        }
        public static void Main(string[] args)
        {
            Task<List<Dictionary<string, object>>> task = Task.Run(() => GetSelected());
            task.Wait(); // Wait for the task to complete

            List<Dictionary<string, object>> outputData = task.Result;

            // Now you can work with outputData as needed
            foreach (var item in outputData)
            {
                foreach (var kvp in item)
                {
                    Console.WriteLine($"{kvp.Key}: {kvp.Value}");
                }
                Console.WriteLine("-------------");
            }
            Console.ReadKey();
        }

    }
}
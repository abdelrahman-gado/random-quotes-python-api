import xlsxwriter

def create_report(report_list, str_current_date):
  directory_name = "./reports"
  file_path = directory_name + "/" + 'quotes_api_report_' + str_current_date + ".xlsx";
  workbook = xlsxwriter.Workbook(file_path);
  worksheet = workbook.add_worksheet()
  worksheet.write(0, 0, 'Quote ID');
  worksheet.write(0, 1, 'Count');
  
  row = 1
  col = 0
  
  for quote_id, count in report_list:
    worksheet.write(row, col, quote_id)
    worksheet.write(row, col+1, count)
    row += 1
  
  workbook.close()
  
  return file_path

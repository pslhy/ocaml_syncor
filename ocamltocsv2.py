import re
def extract_data_from_log(file_name):
     with open(file_name, 'r') as f:
          content = f.read()
          if 'End : Timeout' in content:
               return {'Type': 'Timeout'}
          elif ' End : In Time ' in content:
               processing_time = re.search(r'processing time : :([\d.]+)', content)
               if processing_time:
                processing_time = processing_time.group(1)
               else:
                processing_time = 'N/A'
               if'Error type: noerr' in content:
                    
                   
                    return {'Type': 'No Error', 'Processing Time': processing_time}
               elif 'Error type: lexerr\n---------------------------\n<<<<<<<<<<<<< FINISH >>>>>>>>>>>>' in content:
                    
                   
                    return {'Type': 'Lexer Error','Processing Time': processing_time}
               elif 'Error type: synerr_stop\n---------------------------\n<<<<<<<<<<<<< FINISH >>>>>>>>>>>>' in content:
               
                    
                    return {'Type': 'Syntax Error', 'Processing Time': processing_time}

          
     return {'Type': 'Unknown'}
def main():
     output = []
     for i in range(0,427):
          file_name = f"/home/wangao/lab_work/checkml/syncor/log/syncor3/log_{i}_case.txt"
          data = extract_data_from_log(file_name)
          data['File Number'] =i
          output.append(data)
     with open('output.csv','w') as out_file:
          out_file.write('File Number,Type,Processing Time,Error\n')
          for row in output:
               out_file.write(f"{row.get('File Number')},{row.get('Type')},{row.get('Processing Time', '')},{row.get('Error', '')}\n")
if __name__ == '__main__':
     main()




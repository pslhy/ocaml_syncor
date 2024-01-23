

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from collections import deque
import os
import re
import subprocess
import time
import sys
import subprocess
import tempfile
import time

tokenizer = AutoTokenizer.from_pretrained('sadiqj/camlcoder', trust_remote_code=True, max_length=256, use_safetensors=True)
model = AutoModelForCausalLM.from_pretrained('sadiqj/camlcoder', trust_remote_code=True, use_safetensors=True).to(device='cuda:0', dtype=torch.bfloat16)





import math





import torch.nn.functional as F




def next_tokens(text):
     inputs = tokenizer.encode(text, return_tensors = "pt").to(device='cuda:0')
     with torch.no_grad():
          logits = model(inputs).logits
     probabilities = F.softmax(logits, dim=-1)
     last_token_probabilities = probabilities[0, -1, :]
     
     
     top_k_probabilities, top_k_indices = torch.topk(last_token_probabilities, 1)
     top5_tokens = [tokenizer.decode([idx.item()]) for idx in top_k_indices]

     return top5_tokens, top_k_probabilities



def extract_error_info(error_information, inputCode):
     pattern = r"loc_end = \{[^}]*pos_cnum = (\d+)"
     

     
     

     if "Lexer.Error" in error_information:
          
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Lexer.Errorr", end_pos, len(inputCode))
     elif "Syntaxerr.Other" in error_information:
          
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Other", end_pos, len(inputCode))
     elif "Syntaxerr.Unclosed" in error_information:
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Unclosed", end_pos, len(inputCode))     
     elif "Syntaxerr.Expecting" in error_information:
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Expecting", end_pos, len(inputCode))
     elif "Syntaxerr.Not_expecting" in error_information:
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Not_expecting", end_pos, len(inputCode))
     elif "Syntaxerr.Applicative_path" in error_information:
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Applicative_path", end_pos, len(inputCode))
     
     elif "Syntaxerr.Applicative_path" in error_information:
          match = re.search(pattern, error_information)

          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Applicative_path", end_pos, len(inputCode))
     elif "Syntaxerr.Variable_in_scope" in error_information:
     
          match = re.search(pattern, error_information)
          if match:
          
               end_pos = int(match.group(1))
               return ("Syntaxerr.Variable_in_scope", end_pos, len(inputCode))
     elif "Syntaxerr.Ill_formed_ast" in error_information:
     
          match = re.search(pattern, error_information)
          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Ill_formed_ast", end_pos, len(inputCode))
     elif "Syntaxerr.Invalid_package_type" in error_information:
     
          match = re.search(pattern, error_information)
          if match:
               
               end_pos = int(match.group(1))
               return ("Syntaxerr.Invalid_package_type", end_pos, len(inputCode))
     elif "Syntaxerr.Removed_string_set" in error_information:

          match = re.search(pattern, error_information)
          if match:
               end_pos = int(match.group(1))
               return ("Syntaxerr.Removed_string_set", end_pos, len(inputCode))
     return None


# In[49]:


def runOcamlScript(st):
     temp_file_path = "/home/wangao/lab_work/checkml/syncor/tmp1"
     with open(temp_file_path, 'w+') as temp_file:
          temp_file.write(st)
     if os.path.exists(temp_file_path):          
          ocamlScirpt = '/home/wangao/lab_work/checkml/syncor/syntaxErrorCheck.ml'
          process = subprocess.Popen(['ocaml', ocamlScirpt], 
                                   stdin=subprocess.PIPE, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text = True
                                   )
          output,error = process.communicate(input=st)
          
          if error:
               error_info = extract_error_info(error, st)
     
               if error_info:  # Check if error_info is not None
                    error_type, end_pos, code_length = error_info
                    if "Lexer.Error" in error_type :
                         return True,"lexerr"
                    elif "Syntaxerr" in error_type:
                         
                         if end_pos == code_length:
                              return True,"synerr_continue"
                         
                         else:
                              return False,"synerr_stop"
                         
                              
                              
                    
               
          return True,"noerr"


# In[50]:


class tokenSet:
     def __init__(self, ifeos , string):
          self.ifeos = ifeos
          self.string = string
     
     def __repr__(self):
          return f"(self.probalitity_value, self.string)"








def print_token(token,probabilities,file_path):
     with open(file_path, "a") as file:
          file.write(f"Next Token : {token}, Posbility: {probabilities:.4f}\n") 
          






# import sys
# import os
# for index in range(427):  # 从0到426
#      file_name = f"log_{index}_case.txt"
#      file_path = os.path.join(directory_path, file_name)     
#      with open(file_path, "w") as file:
#           file.write(f"<<<<<<<<<<<< {index} problem >>>>>>>>>>>\n\n\n\n\n")


# In[ ]:





# In[53]:


directory_path= "/home/wangao/lab_work/checkml/syncor/log/baseline3"


# In[54]:


def generate_ocaml_code(file_path,s_text):


     S = []
     
     s= s_text.replace("python","")
     s1 = tokenSet(0, s)

     S.append(s1)
     start_time = time.time()
     while S:
          

          
          s = S.pop()
          with open(file_path, "a") as file:
               file.write(f"code:\n {s.string}\n")
          #    result,errtype = runOcamlScript(s.string)
          #    with open(file_path, "a") as file:
          #           file.write(f"Error type: {errtype}\n")
          #           file.write("---------------------------\n")
          #    if(result == False):
               
          #      continue
          

          t_tokens,top_k_probabilities = next_tokens(s.string) 
          
          
          length = len(t_tokens)  
          
          token = t_tokens[0]
     #for i,token in enumerate(t_tokens):
          
     
          if token == "<|endoftext|>" or token == "\n\n":  
               current_time = time.time()
               process_time = current_time - start_time
               result,errtype = runOcamlScript(s.string)
               with open(file_path, "a") as file:
                    file.write(f"Error type: {errtype}\n")
                    file.write("---------------------------\n")
               with open(file_path, "a") as file:
                    file.write("<<<<<<<<<<<<< FINISH >>>>>>>>>>>>\n\n\n\n")
                    file.write(f"----------END--------\n\nprocessing time : :{process_time}")
               return s.string
               #check and return
               
          st = s.string + token
          newst = tokenSet(0, st)
          S.append(newst)
          
          print_token(token, top_k_probabilities[0].item(),file_path)

               
                    


               #elif error_position is not None:
                    # 去除所有error pos及以其为前缀的内容
                         
                    #S = [state for state in S if not is_prefix(state.string, error_position, st)]

          with open(file_path, "a") as file:
                    file.write("---------------------------\n")                    
     with open(file_path, "a") as file:
                         file.write("----------Other Error--------\n\n")
     return None  # 如果队列为空，返回 None






import make_data_set

     
index = sys.argv[1]
file_name = f"log_{index}_case.txt"
file_path = os.path.join(directory_path, file_name)
text = sys.argv[2]

generate_ocaml_code(file_path,text)





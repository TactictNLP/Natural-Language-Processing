import os

#扫描目录txt文件  保存到一个文件里面
#参数 
#directory 目录
#prefix 前缀
#postfix 后缀
def scan_files(directory,prefix=None,postfix=None):  
    files_list=[]  
      
    for root, sub_dirs, files in os.walk(directory):  
        for special_file in files:  
            if postfix:  
                if special_file.endswith(postfix):  
                    files_list.append(os.path.join(root,special_file))  
            elif prefix:  
                if special_file.startswith(prefix):  
                    files_list.append(os.path.join(root,special_file))  
            else:  
                files_list.append(os.path.join(root,special_file))                          
    return files_list

def save_files_to_file(directory,prefix=None,postfix=None,objectfile=None):
    files = scan_files(directory,prefix,postfix)
    file  = open(objectfile,"wb")
    for f in files:
        print(f)
        file.write(open(f,"rb").read());
    
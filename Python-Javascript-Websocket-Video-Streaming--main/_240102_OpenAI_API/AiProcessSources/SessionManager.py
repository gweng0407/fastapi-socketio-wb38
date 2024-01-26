# -*- coding: cp949 
from ast import List
import os
from openai.types.chat import ChatCompletionMessageParam

import json

from Addon.CustomConsolePrinter import printError, printNor, printProcess


# ���� ��ü
class Session ():
    # ������ �ҷ���. �ҷ����� �迡 ���� ���� �ʱ�ȭ�� ��� ���
    def __init__(self, sid : str, lectureName : str) :
        
        user_documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        saveDirectory = "WB38\\Sessions"
        rootPath = f"{user_documents_path}\\{saveDirectory}"
        
        if not os.path.exists(rootPath):
            os.makedirs(rootPath)
                
        # �ʱ�ȭ
        self.lectureName : str = lectureName
        self.hashValue : str = str(sid) + lectureName
        self.sessionFile : str = f"{rootPath}\\{str(self.hashValue)}.json"
        self.sessionData : ChatCompletionMessageParam  = []
        
        #�ε�
        if(os.path.exists(self.sessionFile)) : #�̹� ���� �������� �ִ� ����
            self.Load()
        else :
            self.Init()
            
    # ���ο� ������ ����
    def Init(self) :
        with open(self.sessionFile, 'w', encoding='utf-8') as file:
            json.dump([], file)
            
        self.Append("system", "�ʴ� ���� ���뿡 ���� ����� ����ڿ��� �亯�� �����ϴ� ģ���� ����̾�.")
        
        self.Save()
    
    # ���� ���� ������ ������
    def Save(self) :
        with open(self.sessionFile, "w", encoding="utf-8") as file:
            json.dump(self.sessionData, file, ensure_ascii=False, indent=2)
          
    # ����� ���� ������ �ҷ���
    def Load(self):
        session = []
        try:
            with open(self.sessionFile, "r", encoding="utf-8") as file:
                session : ChatCompletionMessageParam = json.load(file)
            
        except FileNotFoundError as e:
            printError(f"���� ������ �ҷ����µ��� �����߽��ϴ�. : {e}{e.with_stacktrace().format_exc()}")
            return
            
        self.sessionData = session
    
        
    # ���ο� ��ȭ ������ ����
    def Append(self, role :str, content : str) :
        self.Load();
        self.sessionData.append({"role" : role, "content" : content })
        
        self.Save();
    
    # ����
    def Remove(self) :
        try :
            os.remove(self.sessionFile)
            del self
            return True
        
        except Exception as ex:
            printError(f"{ex}\n{ex.with_traceback.format_exc()}")
            return False

    # ���� ���� �ε�
    def GetData(self) :
        return self.sessionData
    
    def GetLastRole(self) :
        return self.sessionData[len(self.sessionData) - 1]["role"] if len(self.sessionData) != 0 else ""

        
class SessionManagerV2 () :
    def __init__(self) :
        self.pm = None;
        
        user_documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
        saveDirectory = "WB38\\Sessions"
        rootPath = f"{user_documents_path}\\{saveDirectory}"

        self.sessionList : List = [f for f in os.listdir(rootPath) if os.path.isfile(os.path.join(rootPath, f))];
   
    def GetSession(self, sid : str, lectureName : str) :
        return Session(sid, lectureName)
    

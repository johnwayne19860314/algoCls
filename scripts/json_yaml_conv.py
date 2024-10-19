import yaml
import json
import os
from pathlib import Path
from fnmatch import fnmatchcase


class Yaml_Interconversion_Json:
    def __init__(self):
        self.filePathList = []

    # yaml文件内容转换成json格式
    def yaml_to_json(self, yamlPath):
        with open(yamlPath, encoding="utf-8") as f:
            datas = yaml.load(f, Loader=yaml.FullLoader)
        jsonDatas = json.dumps(datas, indent=5)
        # print(jsonDatas)
        return jsonDatas

    # json文件内容转换成yaml格式
    def json_to_yaml(self, jsonPath):
        with open(jsonPath, encoding="utf-8") as f:
            datas = json.load(f)
        yamlDatas = yaml.dump(datas, indent=5, sort_keys=False)
        # print(yamlDatas)
        return yamlDatas

    # 生成文件
    def generate_file(self, filePath, datas):
        if os.path.exists(filePath):
            os.remove(filePath)
        with open(filePath, 'w') as f:
            f.write(datas)

    # 清空列表
    def clear_list(self):
        self.filePathList.clear()

    # 修改文件后缀
    def modify_file_suffix(self, filePath, suffix):
        dirPath = os.path.dirname(filePath)
        fileName = Path(filePath).stem + suffix
        newPath = dirPath + '/' + fileName
        # print('{}_path：{}'.format(suffix, newPath))
        return newPath

    # 原yaml文件同级目录下，生成json文件
    def generate_json_file(self, yamlPath, suffix='.swagger.json'):
        jsonDatas = self.yaml_to_json(yamlPath)
        jsonPath = self.modify_file_suffix(yamlPath, suffix)
        # print('jsonPath：{}'.format(jsonPath))
        jsonpath_ = jsonPath.replace("Charging_Infrastructure","JSON_Files/Energy_Infra")
        self.generate_file(jsonpath_, jsonDatas)

    # 原json文件同级目录下，生成yaml文件
    def generate_yaml_file(self, jsonPath, suffix='.yaml'):
        yamlDatas = self.json_to_yaml(jsonPath)
        yamlPath = self.modify_file_suffix(jsonPath, suffix)
        # print('yamlPath：{}'.format(yamlPath))
        self.generate_file(yamlPath, yamlDatas)

    # 查找指定文件夹下所有相同名称的文件
    def search_file(self, dirPath, fileName):
        dirs = os.listdir(dirPath)
        for currentFile in dirs:
            absPath = dirPath + '/' + currentFile
            if os.path.isdir(absPath):
                self.search_file(absPath, fileName)
            elif currentFile == fileName:
                self.filePathList.append(absPath)

    # 查找指定文件夹下所有相同后缀名的文件
    def search_file_suffix(self, dirPath, suffix):
        dirs = os.listdir(dirPath)
        for currentFile in dirs:
            absPath = dirPath + '/' + currentFile
            if os.path.isdir(absPath):
                if fnmatchcase(currentFile, '.*'):
                    pass
                else:
                    self.search_file_suffix(absPath, suffix)
            elif currentFile.split('.')[-1] == suffix:
                self.filePathList.append(absPath)

    # 批量删除指定文件夹下所有相同名称的文件
    def batch_remove_file(self, dirPath, fileName):
        self.search_file(dirPath, fileName)
        print('The following files are deleted：{}'.format(self.filePathList))
        for filePath in self.filePathList:
            if os.path.exists(filePath):
                os.remove(filePath)
        self.clear_list()

    # 批量删除指定文件夹下所有相同后缀名的文件
    def batch_remove_file_suffix(self, dirPath, suffix):
        self.search_file_suffix(dirPath, suffix)
        print('The following files are deleted：{}'.format(self.filePathList))
        for filePath in self.filePathList:
            if os.path.exists(filePath):
                os.remove(filePath)
        self.clear_list()

    # 批量将目录下的yaml文件转换成json文件
    def batch_yaml_to_json(self, dirPath):
        self.search_file_suffix(dirPath, 'yaml')
        print('The converted yaml file is as follows：{}'.format(self.filePathList))
        for yamPath in self.filePathList:
            try:
                self.generate_json_file(yamPath)
            except Exception as e:
                print('YAML parsing error：{}'.format(e))
        self.clear_list()

    # 批量将目录下的json文件转换成yaml文件
    def batch_json_to_yaml(self, dirPath):
        self.search_file_suffix(dirPath, 'json')
        print('The converted json file is as follows：{}'.format(self.filePathList))
        for jsonPath in self.filePathList:
            try:
                self.generate_yaml_file(jsonPath)
            except Exception as e:
                print('JSON parsing error：{}'.format(jsonPath))
                print(e)
        self.clear_list()


if __name__ == "__main__":
    filePath = './scripts/openapi.yaml'
    yaml_interconversion_json = Yaml_Interconversion_Json()
    yaml_interconversion_json.generate_json_file(filePath)



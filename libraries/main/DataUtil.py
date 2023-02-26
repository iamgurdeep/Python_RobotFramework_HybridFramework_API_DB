# Its heart of Dynamic Json creation . Mapper function build json dinamically based on datasheet input .-Gurdeep
from libraries.main.Main import Main
import json, re
from robot.api.deco import library

tools: Main = Main()


@library
class DataUtil:
    def __init__(self, cfg_sheet_name: str, data_sheet_name: str):
        '''
       This init function will set which API configuration sheet part of main config file that needs to be used
       also set API data sheet part of main data file
       :param cfg_sheet_name: API configuration sheet from main configuration file
       :param data_sheet_name: API data sheet from main data file
       '''
        self.cfg_sheet_name = cfg_sheet_name
        self.data_sheet_name = data_sheet_name

    def branch(self,tree, vector, value):
        # Convert Boolean
        if isinstance(value, str):
            value = value.strip()

            if value.lower() in ['true', 'false']:
                value = True if value.lower() == "true" else False

        # Convert JSON
        try:
            value = json.loads(value)
        except:
            pass

        key = vector[0]
        arr = re.search('\[([0-9]+)\]', key)

        if arr:

            # Get the index of the array, and remove it from the key name
            arr = arr.group(0)
            key = key.replace(arr, '')
            arr = int(arr.replace('[', '').replace(']', ''))

            if key not in tree:

                # If we dont have an array already, turn the dict from the previous
                # recursion into an array and append to it
                tree[key] = []
                tree[key].append(value \
                                     if len(vector) == 1 \
                                     else self.branch({} if key in tree else {},
                                                 vector[1:],
                                                 value))
            else:

                # Check to see if we are inside of an existing array here
                isInArray = False
                for i in range(len(tree[key])):
                    if tree[key][i].get(vector[1:][0], False):
                        isInArray = tree[key][i][vector[1:][0]]

                if isInArray and arr < len(tree[key]) \
                        and isinstance(tree[key][arr], list):
                    # Respond accordingly by appending or updating the value
                    tree[key][arr].append(value \
                                              if len(vector) == 1 \
                                              else self.branch(tree[key] if key in tree else {},
                                                          vector[1:],
                                                          value))
                else:
                    # Make sure we have an index to attach the requested array to
                    while arr >= len(tree[key]):
                        tree[key].append({})

                    # update the existing array with a dict
                    tree[key][arr].update(value \
                                              if len(vector) == 1 \
                                              else self.branch(tree[key][arr] if key in tree else {},
                                                          vector[1:],
                                                          value))

            # Turn comma deliminated values to lists
            if len(vector) == 1 and len(tree[key]) == 1:
                tree[key] = value.split(",")
        else:
            # Add dictionaries together
            tree.update({key: value \
                if len(vector) == 1 \
                else self.branch(tree[key] if key in tree else {},
                            vector[1:],
                            value)})
        return tree

    def build_job(self,data):
        file = [data]
        rowList = []
        for row in file:
            rowObj = {}
            for colName, rowValue in row.items():
                if rowValue:
                    rowObj.update(self.branch(rowObj, colName.split("."), rowValue))
            rowList.append(rowObj)
        return rowList

    def _json_builder(self,jsondata):
        output_json = json.dumps(self.build_job(jsondata), indent=4)
        output_json = json.loads(output_json)
        # # bug fix for list type request
        for key, value in output_json[0].items():
            if not key:
                final_json = value
            elif key:
                final_json = output_json[0]
        return final_json

    def _create_json(self, j_file):
        data_filename, modified_filename = tools.test_fun(j_file=j_file,
                                                          cfg_sheet_name=self.cfg_sheet_name)
        df = tools.read_data_file(datafile_name=data_filename, sheet_name=self.data_sheet_name)
        jsondata = df[j_file].to_dict()
        modifiedjson = self._json_builder(jsondata=jsondata)
        # print(modifiedjson)
        with open(modified_filename, "w") as outfile:
            json.dump(modifiedjson, outfile, indent=2)

    def _data_mapper(self):
        files_to_modify = tools.json_to_modify(cfg_sheet_name=self.cfg_sheet_name)
        for i in range(len(files_to_modify)):
            print(f'Modifying json file {files_to_modify[i]}')
            self._create_json(files_to_modify[i])

# cfg_sheet_name = 'Tax'
# data_sheet_name = 'Tax'
# c =DataUtil(cfg_sheet_name=cfg_sheet_name,data_sheet_name=data_sheet_name)
# c._data_mapper()

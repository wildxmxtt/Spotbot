 ###Update grab_past_flag#####
        filename = "setup.json"
        dictObj = []

    # Check if file exists
        if path.isfile(filename) is False:
            raise Exception("File not found")
    
    # Read JSON file
        with open(filename) as fp:
            dictObj = json.load(fp)
    
    # Verify existing dict
        print(dictObj)

        print(type(dictObj))
        # "grab_past_flag" : 0
        dictObj.update({"grab_past_flag": 1 })
    
    # Verify updated dict
        print(dictObj)
    
        with open(filename, 'w') as json_file:
            json.dump(dictObj, json_file, 
                        indent=4,  
                        separators=(',',': '))
    
        print('Successfully updated setup.json')
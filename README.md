
#  Data Generator

The synthetic data generator takes a config file as an and creates file for each schema provided in the input.



## Sample config

```json
[{
		"filename": "Test_Data_Gen_1",
		"num_rows": 100,
		"format": {
			"type": "csv",
			"delimiter": "|",
			"extension": "txt"
		},
		"db_type": {
			"type": "postgres",
			"username": "",
			"password": "",
			"host": "",
			"database": "",
			"schema": "",
			"port": 5432
		},
		"schema": {
			"Id": {
				"type": "number",
				"is_unique": "yes",
				"is_null": "no"
			},
			"Name": {
				"type": "text"
			}
		}
	},
	{
		"filename": "Test_Data_Gen_2",
		"num_rows": 100,
		"schema": {
			"Age": {
				"type": "int",
				"minvalue": 1,
				"maxvalue": 150
			},
			"is_Indian": {
				"type": "boolean",
				"is_yes_no": false
			}
		}
	}
]
```

The config file in a list of jsons, that contains different keys like filename, num_rows,schema,format,db_type.

The format and db_type keys are optional, as you can see in the above config,
* The first json provides info about all the keys and it specifies what format do the file need to be and in which database a table need to be created
* The second json provides the basic info like filename and number of rows it should have and its schema.
Note: By default csv file format is used to save the data as a file.




## Features

- Data is saved as files
- Data is saved as tables
- The created files can be stored in remote location like S3, SFTP server.

The information about S3 and SFTP are provided to the code through the config file.

```json
{
  "sftp_host": "",
  "port": 22 ,
  "username": "",
  "password": "",
  "region_name": "",
  "access_key_id": "" ,
  "secret_access_key": ""
}
```


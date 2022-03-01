# .Net To Net Core Migration Report Generator

Welcome to the com.castsoftware.uc.net.to.netcore.reports wiki!

>Warning: The Extension described in this document is delivered as-is. This Extension is made available by CAST User Community and governed by Open Source License. Please consider all necessary steps to validate and to test the Extension in your environment before using it in production.        
The extension is published under GNU LGPL v3 open source license

# Introduction

## In what situation should you install this extension?
This extension is a client-specific User community extension
When your application needs an assessment on the effort necessary to migrate it from .Net application to .Net Core.
The extension will flag all the incompatible assemblies that will require to be replaced before the platform change. 

**An up and running CAST Imaging instance is mandatory to generate this report.**

# CAST AIP compatibility

This extension is compatible with all AIP versions from 8.3.3 + and will be also in future versions.
It relies on Extension SDK API, and comes with its own AIP upgrade (backward compatible)

# Supported DBMS servers

This extension is compatible with the following DBMS servers (hosting the Analysis Service):

This extension is compatible with the following DBMS servers (hosting the Analysis Service):

| CAST AIP release       | CSS3 | CSS4 | PG on Linux|
| -----------------------|:----:|:------:|:--------: |
| All supported releases |   ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)  |    ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)   |    ![Supported](https://github.com/CAST-Extend/resourceALT/blob/master/check.png)    | 

# Configuration instructions for the report generation
- Run an analysis using this AIP Extension and export the application on CAST Imaging

- Make sure Python 3.9 in installed on your local machine (Windows : https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe )
    - Make sure to check **use System PATH** during the installation
    - Install PIP along with 

- Open a command prompt and navigate to the folder containing to this extension.
    - Execute `pip.exe install -r requirements.txt`

- Go to configuration\application.ini
    - Modify the parameters if necessary ( e.g.: Imaging connection string, application name )
    - Make sure the name of the application is correct ( It should match the name in CAST Imaging URL )
    - Make sure the working directory specified in the configuration, exists on your machine ( create it otherwise )

- Launch the .NetToNetCore script 
    - Execute `python39.exe main.py`

- The reports will be generated and stored in the specified working directory



# Operation instructions

## Source preparation and analysis configuration instructions
Extension  will work  at application level (after all analyzers)

## Analysis Dependency 
    
    product SQL Analyzer >= 2.1.0
   
* Check Application Unit content
   ![](https://github.com/CAST-Extend/com.castsoftware.labs.db2Postgresqlmigration/blob/master/log.png)
  * properties created will be reported in the log. The content will also reflect this.

## List of generated reports
- .Net to .Net Core Non-compatible method used + effort estimate 
- .Net to .Net Core Non-compatible assemblies used + effort estimate 
- AspX decommission effort estimate 
- Razor To Blazor effort estimate  

# Known issues

- None reported

# Limitations and potential enhancements

# Versions

## Version 1.0.0 Release Notes

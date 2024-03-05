import yaml
############## Import /opt/SVTECH-Junos-Automation/module_utils/PYEZ_BASE_FUNC.py ######################
# Load config path from file
config = yaml.load(open('app_config.yml',"r"), Loader=yaml.FullLoader)
print(config.get('path_module_utils'))

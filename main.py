# Driver Code.
import yaml

# Local modules.
import Parser
import results

if __name__ == '__main__':
    # Read Config.
    with open("config.yaml", "r", encoding = 'utf-8') as ymlfile:
        config = yaml.safe_load(ymlfile)
    
    # Run parser.
    Parser.parse_rawfile(config)
    
    # Return Results in PDF.
    results.generate_result(config)
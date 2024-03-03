import data_generation
import openai




openai.api_key = ''

output_file_path = 'output.csv'

QUERY = "Solve\n\\[\\arcsin x + \\arcsin 2x = \\frac{\\pi}{3}.\\]" 

ROLES = ["Mathematician", "Economist", "Programmer", "Historian"]
#need function that gives us the role description based off of the key 

def main():
    data_generation.construct_training_data(QUERY, ROLES, data_generation.ROLE_MAP, openai, output_file_path)
    


if __name__ == "__main__":
    main()


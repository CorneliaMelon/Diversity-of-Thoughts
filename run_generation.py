import data_generation
import openai




openai.api_key = ''

output_file_path = 'output.csv'

QUERY = "A standard six-sided fair die is rolled four times. The probability that the product of all four numbers rolled is a perfect square is $\\tfrac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m+n$.\n" 

ROLES = ["Mathematician", "Economist", "Programmer", "Historian"]
#need function that gives us the role description based off of the key 

def main():
    data_generation.construct_training_data(QUERY, ROLES, data_generation.ROLE_MAP, openai, output_file_path)
    


if __name__ == "__main__":
    main()


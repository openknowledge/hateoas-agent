# HATEOAS Agent
This project implements an AI agent designed to autonomously explore and interact with RESTful APIs that follow the HATEOAS (Hypermedia as the Engine of Application State) constraint. The agent leverages hypermedia links provided by the API to discover available actions and resources without prior knowledge of the API structure.

# How to start
## Start Spring Restbucks
In order to test the agent, we need a HATEOAS compatible API to interact with. You can use i.e. [Spring Restbucks](https://github.com/odrotbohm/spring-restbucks).
```
git clone https://github.com/odrotbohm/spring-restbucks.git
cd spring-restbucks
git reset --hard d215c68534505822f637a328eb7485c246c95041
cd server
mvn clean package
java -jar target/*.jar
```
After starting Spring Restbucks you can use the HAL-Explorer to add some data (i.e. drinks or orders) if you like. If url of the API is not `http://localhost:8080/`, please update the variable `ENTRY_POINT` in `prompts.py`.

## Start AI Agent
1. We use [openai-agents](https://github.com/openai/openai-agents-python) library. Therefore you have to set the `OPENAI_API_KEY` environment variable.
2. For dependency management we use [uv](https://docs.astral.sh/uv/getting-started/).
3. Setup project by `uv sync`
4. Run the agent by `uv run agent.py --prompt "Who are you?"`
5. Change the value of the command line argument `--prompt` as you like. Below, you find some examples.

## Example Prompts
* "How many orders are there?"
* "What is the total amount to be paid?"
* "Which drinks do we have available?"
* "Create a new drink called MySpecialDrink! It should cost 50 cent."
* "Update the price of MySpecialDrink. It should cost 2 Euro now!" 
* "Delete the MySpecialDrink. We do not sell it anymore!"

# Questions?
Please contact [Tim Wüllner](https://www.linkedin.com/in/tim-wuellner/) or [Arne Limburg](https://www.linkedin.com/in/arnelimburg/).
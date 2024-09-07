# Stock Price & News Analysis Application

Esta aplicação foi desenvolvida durante o evento **Imersão IA**, promovido pela **Rocketseat**, com o objetivo de criar um sistema avançado de análise de preços de ações e notícias de mercado. O projeto utiliza diversas ferramentas de inteligência artificial, APIs e bibliotecas de finanças, permitindo a criação de relatórios detalhados sobre tendências de ações e notícias relacionadas.

## Tecnologias Utilizadas

### 1. **Python**
A linguagem principal utilizada no projeto foi Python, uma das mais populares no mundo da inteligência artificial e análise de dados, devido à sua vasta gama de bibliotecas e facilidade de integração com APIs.

### 2. **YFinance**
Utilizada para obter dados financeiros históricos, como o preço de ações de uma empresa ao longo de um período específico. A função `fetch_stock_price()` utiliza o **Yahoo Finance API** para realizar a consulta das cotações.

### 3. **Crew AI**
O CrewAI é uma biblioteca projetada para facilitar a criação e o gerenciamento de agentes de IA que colaboram para atingir um objetivo. Cada agente é configurado com uma função específica, podendo executar tarefas de forma independente ou coordenada, usando processamento hierárquico para dividir o trabalho. Isso permite uma abordagem modular para projetos de IA, onde diferentes aspectos de um problema são resolvidos por agentes especializados.

#### Uso no projeto:
- Obtenção de preços de ações a partir de um ticker fornecido (ex: AAPL para Apple).
- Análise histórica de dados de ações de um ano para prever tendências.

```python
stock = yf.download("ticket", start="2023-20-08", end="2024-20-08")

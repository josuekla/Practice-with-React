# 📋 Task Manager (Gerenciador de Tarefas)

Este projeto é uma aplicação de gerenciamento de tarefas desenvolvida durante um curso de React. O objetivo principal foi aprender os fundamentos da biblioteca, gerenciamento de estado e roteamento.

## 🚀 Tecnologias Utilizadas

- **React** (Vite)
- **Tailwind CSS** (Estilização)
- **React Router Dom** (Navegação)
- **Lucide React** (Ícones)

## 🧠 O que eu aprendi

Durante o desenvolvimento deste projeto, coloquei em prática os seguintes conceitos:

### 1. Componentização e Props
Aprendi a dividir a aplicação em pequenas partes reutilizáveis.
- Criação de componentes isolados como [`Input.jsx`](src/components/Input.jsx) e [`Button.jsx`](src/components/Button.jsx).
- Uso de **Props** para passar dados do componente pai (`App.jsx`) para os filhos (ex: passar a lista de tarefas para [`Tasks.jsx`](src/components/Tasks.jsx)).
- Uso da prop especial `children` para criar componentes flexíveis como o [`Title.jsx`](src/components/Title.jsx).

### 2. React Hooks (Estado e Efeitos)
- **useState**: Utilizado para gerenciar o estado das tarefas, os inputs do formulário e mensagens de erro em [`AddTask.jsx`](src/components/AddTask.jsx).
- **useEffect**: Implementado em [`App.jsx`](src/App.jsx) para persistir as tarefas no **LocalStorage**, garantindo que os dados não sejam perdidos ao recarregar a página.

### 3. Manipulação de Listas e Eventos
- Uso do método `.map()` para renderizar a lista de tarefas dinamicamente.
- Manipulação de eventos de formulário (`onSubmit`) e cliques (`onClick`) para adicionar e remover tarefas.
- Validação simples de formulário para impedir tarefas vazias.

### 4. Roteamento (React Router Dom)
Implementação de navegação entre páginas sem recarregar o navegador.
- Configuração de rotas no [`main.jsx`](src/main.jsx).
- Uso do hook `useNavigate` para navegação programática.
- Uso do hook `useSearchParams` em [`TaskPage.jsx`](src/pages/TaskPage.jsx) para ler dados passados via URL (Query Params) e exibir os detalhes da tarefa.

### 5. Estilização com Tailwind CSS
- Utilização de classes utilitárias para criar um layout responsivo e agradável.
- Estilização condicional (ex: riscar o texto quando a tarefa está completa).

## ✨ Funcionalidades

- [x] Adicionar novas tarefas com título e descrição.
- [x] Listar tarefas existentes.
- [x] Ver detalhes de uma tarefa em uma página separada.
- [x] Excluir tarefas.
- [x] Persistência de dados no navegador (LocalStorage).
- [x] Validação de campos obrigatórios.

## 📂 Estrutura do Projeto

O código principal está organizado da seguinte forma:

- `src/App.jsx`: Componente principal e lógica de estado.
- `src/pages/`: Contém as páginas da aplicação (ex: Detalhes da Tarefa).
- `src/components/`: Componentes reutilizáveis (Botões, Inputs, Lista).

## 🔧 Como rodar o projeto

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   npm install
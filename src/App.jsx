import { useEffect, useState } from "react";
import AddTask from "./components/AddTask";
import Tasks from "./components/Tasks";

import "./App.css";
import Title from "./components/Title";

function App() {
  // States (Estado)

  const [tasks, setTasks] = useState([]);

  // Pega a URL da API das variáveis de ambiente ou usa localhost como fallback
  const API_URL = import.meta.env.VITE_API_URL;

  // Carregar tarefas da API ao iniciar
  useEffect(() => {
  async function fetchTasks() {
    try {
      console.log("Buscando em:", `${API_URL}/tasks`);

      const response = await fetch(`${API_URL}/tasks`);

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log("Dados recebidos:", data);

      setTasks(data);
    } catch (error) {
      console.error("Erro ao buscar tarefas:", error);
    }
  }

  fetchTasks();
}, [API_URL]);

  
  async function onTaskClick(taskId) {
    try {
      // Chama a API para atualizar no banco
      await fetch(`${API_URL}/tasks/${taskId}/toggle`, {
        method: "PATCH",
      });

      // Atualiza a interface localmente
      const updatedTasks = tasks.map((task) => {
        if (task.id === taskId) {
          return { ...task, isCompleted: !task.isCompleted };
        }
        return task;
      });
      setTasks(updatedTasks);
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
    }
  }


  async function handleDelete(taskId) {
    try {
      // Chama a API para deletar
      await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "DELETE",
      });

      // Remove da lista local
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error);
    }
  }



  async function SubmitTask(title, description) {
    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          description,
          isCompleted: false,
          created_at: new Date().toLocaleString("pt-BR", {
          timeZone: "America/Sao_Paulo"
})

        }),
      });

      const newTask = await response.json();
      setTasks((prevTasks) => [...prevTasks, newTask]);
    } catch (error) {
      console.error("Erro ao criar tarefa:", error);
    }
  }



  // let message = "Good morning!";
  return (
    <div className="w-screen min-h-screen bg-slate-500 flex justify-center p-6 ">
     <div className="w-[500px] space-y-4=6">
      <Title>Task Manager</Title>
      <AddTask test={SubmitTask}/>

      <Tasks tasks={tasks} onTaskClick={onTaskClick} handleDelete={handleDelete} />

     </div>
    </div>
  )
}

export default App;
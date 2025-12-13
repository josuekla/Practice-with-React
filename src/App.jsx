import { useEffect, useState } from "react";
import AddTask from "./components/AddTask";
import Tasks from "./components/Tasks";
import ConfirmModal from "./components/ConfirmModal";

import "./App.css";
import Title from "./components/Title";

function App() {
  // States (Estado)
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState(null);


  const [tasks, setTasks] = useState(JSON.parse(localStorage.getItem("tasks")) || []);

  useEffect(() => {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }, [tasks]);


  // Quando passamos a array de dependências vazia, o useEffect só é executado uma vez, quando o componente é montado.
 useEffect(() => {
  // async function fetchInitialTasks() {
  //   const response = await fetch(
  //     "https://jsonplaceholder.typicode.com/todos?_limit=10"
  //   );
  //   if (!response.ok) {
  //     throw new Error("Failed to fetch tasks");
  //   }
  //   const data = await response.json();
  //   setTasks(data)
  //   console.log(data);
  // }

  // fetchInitialTasks();
}, []);

  
  function onTaskClick(taskId) {
    const updatedTasks = tasks.map((task) => {
      if (task.id === taskId) {
        return {...task, isCompleted: !task.isCompleted };
  }
  return task;
    });
    setTasks(updatedTasks);
  }

  function handleRequestDelete(taskId) {
  setTaskToDelete(taskId);
  setShowConfirmation(true);
  }

  function handleDelete() {
  setTasks(prevTasks =>
    prevTasks.filter(task => task.id !== taskToDelete)
  );

  setShowConfirmation(false);
  // setTaskToDelete(null);
  }


  function SubmitTask(title, description) {
    const newTask = {
      id: Date.now(),
      title,
      description,
      isCompleted: false,
      createdAt: new Date()
    };
    setTasks((prevTasks) => [...prevTasks, newTask]);
    console.log("Task added:", newTask.id, newTask.title, newTask.description, newTask.createdAt);
  }



  // let message = "Good morning!";
  return (
    <div className="w-screen min-h-screen bg-slate-500 flex justify-center p-6 ">
     <div className="w-[500px] space-y-4=6">
      <Title>Task Manager</Title>
      <AddTask test={SubmitTask}/>

      <Tasks tasks={tasks} onTaskClick={onTaskClick} onDeleteRequest={handleRequestDelete} />

      <ConfirmModal 
        open={showConfirmation}
        onConfirm={handleDelete}
        onCancel={() => setShowConfirmation(false)}
      />

     </div>
    </div>
  )
}

export default App;
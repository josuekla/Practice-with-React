import { useState } from "react";
import Input from "./Input.jsx";


function AddTask({test}) {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = (e) => {
    e.preventDefault();

    if (!title.trim() || !description.trim()) {
      setError("Preencha todos os campos antes de adicionar a tarefa.");
      return;
    }

    setError("");
    test(title, description);

    setTitle("");
    setDescription("");
  };

    return (
        <form onSubmit={handleSubmit} className="space-y-3 p-6 bg-gradient-to-b from-blue-500 to-blue-400 shadow rounded-md mt-6 flex flex-col">
            {error && (
                <div className="rounded-md border-l-4 border-red-500 bg-red-100 px-4 py-3 text-sm text-red-700">
                {error}
                </div>
            )}
            <Input 
                type="text"
                placeholder="Digit the title of the task"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
            />
            <Input 
                type="text"
                placeholder="Digit the description of the task"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
            />
            
        <button 
        type="submit"
        className="w-full bg-green-500 hover:bg-green-600 text-white font-bold p-2 rounded-md">
            Add Task
        </button>
        </form>
    )
}

export default AddTask;
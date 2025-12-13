import { ChevronRightIcon, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Button  from "./Button.jsx";

function Task({tasks, handleDelete}) {
    const navigate = useNavigate();

    function onNavigateToDetails(task) {
        const queryParams = new URLSearchParams({
            title: task.title,
            description: task.description,
            isCompleted: task.isCompleted,
            createdAt: task.createdAt
        }).toString();
        navigate(`/task?${queryParams}`);
    }


    const isEmpty = tasks.length === 0;

    return (
        <div>
            {isEmpty ? (
                <div className="p-6 bg-gradient-to-b from-blue-500 to-blue-400 shadow rounded-md mt-6 text-center text-white">
                    Nenhuma tarefa por aqui ainda. Clique em "Add Task" para criar a primeira.
                </div>
            ) : (
                <ul className="space-y-3 p-6 bg-gradient-to-b from-blue-500 to-blue-400 shadow rounded-md mt-6">
                    {tasks.map((task) => (
                        <li key={task.id} className="flex justify-between items-center gap-3">
                            <button 
                                onClick={() => onTaskClick(task.id)}
                                className={` font-medium text-left bg-slate-200 p-2 rounded-md w-full text-left${task.isCompleted ? ' line-through' : ''}`}>
                                {task.title}
                            </button>
                            <Button
                            onClick={() => onNavigateToDetails(task)} 
                            className="bg-slate-200 p-1 rounded-md" >
                                <ChevronRightIcon />
                            </Button>
                            <Button 
                            onClick={() => handleDelete(task.id)}
                            className={`${task.isCompleted ? "" : 'bg-slate-200 p-1 rounded-md'}`} >
                                <Trash2 />
                            </Button>
                        </li>
                        ))}
                </ul>
            )}
        </div>
    )
}


export default Task;
import { useSearchParams, useNavigate} from "react-router-dom";
import { ArrowLeftFromLine } from "lucide-react";
import Title from "../components/Title.jsx";

function TaskPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  return (
    <div className="w-screen h-screen bg-slate-500 flex justify-center p-6 ">
     <div className="w-[500px] space-y-4=6">
        <div className="relative flex items-center justify-center">
        <button
            onClick={() => navigate(-1)}
            className="absolute left-0 mb-4 px-4 py-2 bg-blue-600 text-white  hover:bg-blue-700 rounded-3xl"
        >
            <ArrowLeftFromLine />
        </button>
        <Title>Task details</Title>
        </div>
      
      <div className="flex flex-col gap-3 p-6 bg-gradient-to-b from-blue-500 to-blue-400 shadow-xl rounded-xl mt-6">
            <h2 className="font-bold text-3xl text-white">Título: {searchParams.get("title")}</h2>
            <h2 className="text-xl text-white">Descrição: {searchParams.get("description")}</h2>
            <h2 className=" text-md text-white">Criado em: {new Date(searchParams.get("createdAt")).toLocaleString()}</h2>
        </div>
     </div>
    </div>
  );
}

export default TaskPage;
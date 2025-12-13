function ConfirmModal({open, onConfirm, onCancel}) {
    if (!open) return null;

    return (
    <div className="overflow-auto fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-6 ">
        <div className="bg-white p-6 rounded-md shadow-xl flex flex-col gap-4 h-60 w-96 justify-center">
            <p className="text-center font-bold ">Tem certeza que deseja excluir?</p>

            <button onClick={onConfirm}>Confirmar</button>
            <button onClick={onCancel} className="p-2 text-red-400">Cancelar</button>
        </div>
    </div>
  );
}

export default ConfirmModal;

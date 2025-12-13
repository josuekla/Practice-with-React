function Button(props) {
    return (
        <button
        {...props}
        className="bg-slate-200 p-1 rounded-md"
        
        >
        {props.children}
        </button>
    )
}

export default Button;
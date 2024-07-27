import { ChangeEvent } from "react"

interface Props {
    label: string
    type: "text" | "password" | "number" | "email" | "datetime-local"
    name: string
    id: string
    placeholder: string
    handleChange: (e: ChangeEvent<HTMLInputElement>) => void
    value:string
    min?:string
}

export function Input({ label, type, name, id, placeholder, handleChange,value,min }:Props) {
    return (
        <article>
            <label
                htmlFor={id}
                className="block mb-2 text-sm font-medium text-gray-900 "
            >
                {label}
            </label>
            <input
                type={type}
                name={name}
                id={id}
                value={value}
                min={min}
                onChange={handleChange}
                placeholder={placeholder}
                className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            />
        </article>
    );
}

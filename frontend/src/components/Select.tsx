import { ChangeEvent } from "react";

interface OptionType {
  key:string
  value:string
}

interface Props {
    name:string
    label:string
    value:string
    handleChange:(e: ChangeEvent<HTMLInputElement|HTMLSelectElement>)=>void
    options:OptionType[]
}

export function Select({ name,label,value,handleChange,options }:Props) {
  return (
    <article>
      <label
        htmlFor={name}
        className="block mb-2 text-sm font-medium text-gray-900 "
      >
        {label}
      </label>
      <select
        name={name}
        value={value}
        onChange={handleChange}
        id={name}
        className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
      >
        {
            options.map((element)=>{
                return <option className="capitalize" value={element.key}>{element.value}</option>
            })
        }
      </select>
    </article>
  );
}

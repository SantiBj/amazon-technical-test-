import { ChangeEvent } from "react";

interface Props {
  label: string;
  name: string;
  id: string;
  placeholder: string;
  handleChange: (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void;
  value: string;
}

export function Textarea({
  label,
  name,
  id,
  placeholder,
  handleChange,
  value,
}: Props) {
  return (
    <article>
      <label
        htmlFor={id}
        className="block mb-2 text-sm font-medium text-gray-900"
      >
        {label}
      </label>
      <textarea
        required
        id={id}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
      ></textarea>
    </article>
  );
}

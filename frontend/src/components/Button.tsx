export interface Props {
  name: string;
  onclick:()=>void
}

export function Button({ name,onclick }: Props) {
  return (
    <button onClick={onclick} className="p-[5px] border-black border-[2px] rounded-md">
      {name}
    </button>
  );
}

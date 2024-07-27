import { AiOutlineLoading } from "react-icons/ai";

interface Props {
  loading: boolean;
}

export function Loading({ loading }: Props) {
  return (
    <section
      className={`${
        loading ? "fixed" : "hidden"
      } top-0 bottom-0 z-50 left-0 right-0 z-10 bg-[#ffffffa6] flex justify-center items-center`}
    >
      <section className=" animate-spin">
        <AiOutlineLoading size={40} />
      </section>
    </section>
  );
}

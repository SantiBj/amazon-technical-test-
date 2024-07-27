import { ReactElement } from "react";

interface Props {
    state: boolean;
    children:ReactElement
}

export function Modal({ state, children }: Props) {
    return (
        <article className={`${state ? "" : "hidden"} fixed z-50 top-0 bottom-0 left-0 right-0 bg-[#ffffffb9] flex justify-center items-center`}>
            {children}
        </article>
    );
}

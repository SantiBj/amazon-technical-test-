import { ReactElement } from "react";

export function Page({ children }:{children:ReactElement}){
    return (
        <section className="w-[80%] mx-auto max-w-[1200px]">
            {children}
        </section>
    )
}
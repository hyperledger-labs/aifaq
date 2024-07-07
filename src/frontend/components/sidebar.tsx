import React from 'react'
import MenuOptions from './menu-options'

type Props = {}

const Sidebar = (props: Props) => {
    return (
        <aside className="sticky top-0 overflow-y-auto h-full bg-primary text-white py-1 px-2 w-64 md:block hidden">
            <MenuOptions />
        </aside>
    )
}

export default Sidebar
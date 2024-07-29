import React from "react";
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';

const   DropdownMenuComponent = () => {
    return(
        <DropdownMenu.Root>
            <DropdownMenu.Trigger className="trigger-button">
                Menu
                </DropdownMenu.Trigger>
                <DropdownMenu.Content className="dropdown-content">
                    <DropdownMenu.Item className="dropdown-item">
                        Pin
                    </DropdownMenu.Item>
                    <DropdownMenu.Separator className="dropdown-seperator"/>
                    <DropdownMenu.Item className="dropdown-item">
                        Rename
                    </DropdownMenu.Item>
                    <DropdownMenu.Separator className="dropdown-seperator"/>
                    <DropdownMenu.Item className="dropdown-item">
                        Delete
                    </DropdownMenu.Item>
                </DropdownMenu.Content>
        </DropdownMenu.Root>
    );
};
export default DropdownMenuComponent;
import React from 'react';
import { Button } from './ui/button';
import {
	FilePlus,
	PanelLeft
} from 'lucide-react';

type Props = {
	isOpen: boolean;
	toggleSidebar: () => void;
};

const MenuOptions = (props: Props) => {
	return (
		<div className="h-10 flex flex-row md:justify-between items-center">
			<Button
				size="icon"
				variant="link"
				className="rounded-xl bg-transparent text-background"
			>
				<PanelLeft
					onClick={props.toggleSidebar}
				/>
			</Button>
			<Button
				size="icon"
				variant="link"
				className="rounded-xl bg-transparent text-background"
			>
				<FilePlus />
			</Button>
		</div>
	);
};

export default MenuOptions;

'use client';
import React, {
	useEffect,
	useState
} from 'react';
import MenuOptions from './menu-options';
import { useWindowSize } from '../hooks/useWindowSize';
import { FilePlus, Menu } from 'lucide-react';
import {
	Sheet,
	SheetClose,
	SheetContent,
	SheetDescription,
	SheetFooter,
	SheetHeader,
	SheetTitle,
	SheetTrigger
} from '@/components/ui/sheet';
import SidebarHistory from './sidebar-history';

type Props = {};

const SHEET_SIDES = ['left'] as const;
type SheetSide = (typeof SHEET_SIDES)[number];

const Sidebar = (props: Props) => {
	const [sidebarOpen, setSideBarOpen] =
		useState(true);
	const [showMenuIcon, setShowMenuIcon] =
		useState(false);
	const [isMounted, setIsMounted] =
		useState(false);
	const { isMobile } = useWindowSize({
		initializeWithValue: true
	});

	const handleViewSidebar = () => {
		setSideBarOpen(!sidebarOpen);
	};

	useEffect(() => {
		setIsMounted(true);
	}, [isMounted]);

	useEffect(() => {
		setSideBarOpen(!isMobile);
	}, [isMobile]);

	useEffect(() => {
		if (!sidebarOpen) {
			const timer = setTimeout(() => {
				setShowMenuIcon(true);
			}, 300);

			return () => clearTimeout(timer);
		} else {
			setShowMenuIcon(false);
		}
	}, [sidebarOpen]);

	if (!isMounted) {
		return null;
	}

	return (
		<div className="relative flex">
			{!sidebarOpen && showMenuIcon && (
				<>
					<button
						onClick={handleViewSidebar}
						className="fixed top-0 left-0 mt-1 ml-1 px-1 py-2 text-black rounded z-50 transition-all duration-30 ease-in-out"
					>
						<Menu />
					</button>
				</>
			)}

			{isMobile ? (
				<div>
					{SHEET_SIDES.map((side) => (
						<Sheet key={side}>
							<SheetTrigger asChild>
								<button className="fixed top-0 left-0 mt-1 ml-1 px-1 py-2 text-black rounded z-50 transition-all duration-300 ease-out">
									<Menu />
								</button>
							</SheetTrigger>
							<SheetContent
								side={side}
								className="m-0 p-0"
							>
								<SheetHeader className="m-0 p-0 h-full w-full bg-primary text-white py-1 px-2 transition-transform duration-300 ease-out">
									<div className="h-10 flex flex-row md:justify-between items-center">
										<button className="ml-3 mt-1 rounded-xl bg-transparent text-background">
											<FilePlus />
										</button>
									</div>
									<SidebarHistory />
								</SheetHeader>
							</SheetContent>
						</Sheet>
					))}
				</div>
			) : (
				<>
					<aside
						className={`${
							sidebarOpen
								? 'relative translate-x-0'
								: 'fixed -translate-x-full'
						} top-0 h-full bg-primary text-white py-1 px-2 w-64 transition-transform duration-500 ease-in z-40`}
						style={{
							transitionDelay: '0s',
							transitionDuration: '500ms',
							transitionProperty: 'transform',
							transitionTimingFunction:
								'ease-in-out'
						}}
					>
						<MenuOptions
							isOpen={sidebarOpen}
							toggleSidebar={handleViewSidebar}
						/>
						<SidebarHistory />
					</aside>
				</>
			)}
		</div>
	);
};

export default Sidebar;

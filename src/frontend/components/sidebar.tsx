"use client"
import React, { useEffect, useState } from 'react';
import MenuOptions from './menu-options';
import { useWindowSize } from '../hooks/useWindowSize';
import { Menu } from 'lucide-react';


type Props = {
  isOpen: boolean;
  toggleSidebar: () => void;
};

const Sidebar = (props: Props) => {
  const [sidebarOpen, setSideBarOpen] = useState(true);
  const { isMobile } = useWindowSize({ initializeWithValue: true });

  const handleViewSidebar = () => {
    setSideBarOpen(!sidebarOpen);
  };

  useEffect(() => {
    setSideBarOpen(!isMobile);
  }, [isMobile]);

  return (
    <div>
      <aside
        className={`fixed top-0 h-full bg-primary text-white py-1 px-2 w-64 transition-transform duration-300 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <MenuOptions isOpen={sidebarOpen} toggleSidebar={handleViewSidebar} />
      </aside>
      {!sidebarOpen && (
        <aside className="w-full flex bg-transparent">
          {/* this is button placed in the header of navbar */}
          <button
            onClick={handleViewSidebar}
            className="mt-1 ml-2 px-1 py-2 text-black rounded transition-all duration-300"
          >
            <Menu />
          </button>
        </aside>
      )}
    </div>
  );
};

export default Sidebar;

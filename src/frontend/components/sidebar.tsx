"use client"
import React, { useEffect, useState } from 'react';
import MenuOptions from './menu-options';
import { IoIosArrowForward } from "react-icons/io";

type Props = {
  isOpen: boolean;
  toggleSidebar: () => void;
};

const Sidebar = (props: Props) => {
  const [sidebarOpen, setSideBarOpen] = useState(true);

  const handleViewSidebar = () => {
    setSideBarOpen(!sidebarOpen);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setSideBarOpen(true);
      } else {
        setSideBarOpen(false);
      }
    };

    handleResize(); // Set initial state based on screen size
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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
        <aside className="h-full w-full flex items-center justify-center bg-transparent">
          <button
            onClick={handleViewSidebar}
            className="px-1 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-all duration-300"
          >
            <IoIosArrowForward size={25} />
          </button>
        </aside>
      )}
    </div>
  );
};

export default Sidebar;

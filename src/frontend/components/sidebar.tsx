"use client";
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
  const [showMenuIcon, setShowMenuIcon] = useState(false);
  const { isMobile } = useWindowSize({ initializeWithValue: true });

  const handleViewSidebar = () => {
    setSideBarOpen(!sidebarOpen);
  };

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

  return (
    <div className=''>
      {!sidebarOpen && showMenuIcon && (
        <button
          onClick={handleViewSidebar}
          className="fixed top-0 left-0 mt-1 ml-1 px-1 py-2 text-black rounded z-50 transition-all duration-300"
        >
          <Menu />
        </button>
      )}

      <aside
        className={`fixed top-0 h-full bg-primary text-white py-1 px-2 w-64 transition-transform duration-300 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } z-40`}
      >
        <MenuOptions isOpen={sidebarOpen} toggleSidebar={handleViewSidebar} />
      </aside>
    </div>
  );
};

export default Sidebar;

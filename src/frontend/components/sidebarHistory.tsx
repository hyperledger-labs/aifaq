"use client";
import React, { useEffect, useState } from "react";
import { DropdownMenuCheckboxItemProps } from "@radix-ui/react-dropdown-menu";
import { Button } from "@/components/ui/button";
import {
   DropdownMenu,
   DropdownMenuCheckboxItem,
   DropdownMenuContent,
   DropdownMenuSeparator,
   DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { EllipsisVertical, Pencil, Pin, Trash2 } from "lucide-react";

// Import the mock data
import { historyData as mockHistoryData } from "./historyData";

type Props = {};
type Checked = DropdownMenuCheckboxItemProps["checked"];

const SidebarHistory = (props: Props) => {
   const [showActivityBar, setShowActivityBar] = React.useState<Checked>(false);
   const [historyData, setHistoryData] = useState<
      { id: number; title: string }[]
   >([]);

   //get the data from backend when the backend is ready
   //change the URL according to the backend routes
   // useEffect(() => {
   //    const url = process.env.URL + "/history";

   //    fetch(url)
   //       .then((response) => {
   //          if (!response.ok) {
   //             throw new Error("Network response was not ok");
   //          }
   //          return response.json();
   //       })
   //       .then((data) => {
   //          setHistoryData(data);
   //       })
   //       .catch((error) => {
   //          console.error("Error fetching data:", error);
   //       });
   // }, []);

   useEffect(() => {
      // Set the mock data as the state
      setHistoryData(mockHistoryData);
   }, []);

   const truncateTitle = (title: string) => {
      return title.length > 17 ? title.slice(0, 17) + "..." : title;
   };

   return (
      <div className="mt-10">
         {historyData.map((item) => (
            <div
               key={item.id}
               className="flex justify-between mt-1 p-3 border-none rounded-lg font-semibold bg-slate-800 hover:bg-slate-800 cursor-pointer">
               <div className="my-auto overflow-hidden">
                  {truncateTitle(item.title)}
               </div>

               <button>
                  <DropdownMenu>
                     <DropdownMenuTrigger asChild>
                        <Button
                           variant="outline"
                           className="p-0 m-0 text-white bg-slate-800 hover:bg-slate-800 hover:text-white font-semibold border-none">
                           <EllipsisVertical />
                        </Button>
                     </DropdownMenuTrigger>
                     <DropdownMenuContent className="w-56">
                        <DropdownMenuSeparator />
                        <DropdownMenuCheckboxItem
                           checked={showActivityBar}
                           onCheckedChange={setShowActivityBar}>
                           <Pin className="mr-2" /> Pin
                        </DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>
                           <Pencil className="mr-2" />
                           Rename
                        </DropdownMenuCheckboxItem>
                        <DropdownMenuCheckboxItem>
                           <Trash2 className="mr-2" /> Delete
                        </DropdownMenuCheckboxItem>
                     </DropdownMenuContent>
                  </DropdownMenu>
               </button>
            </div>
         ))}
      </div>
   );
};

export default SidebarHistory;

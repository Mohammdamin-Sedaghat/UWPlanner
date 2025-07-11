"use client";
import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { MdAccountCircle, MdExitToApp } from "react-icons/md";
import { IoMdSettings } from "react-icons/io";
import { useAuth } from "@/app/AuthProvider";
import { useRouter } from "next/navigation";
import HoverEffect from "./HoverEffect";

interface NavbarProps {
    signedIn?: boolean;
    username?: string;
}

const Navbar: React.FC<NavbarProps> = ({
    signedIn = false,
    username = undefined,
}) => {
    const [panelOn, setPanelOn] = useState<boolean>(false);
    const panelRef = useRef<HTMLDivElement>(null);
    const buttonRef = useRef<HTMLDivElement>(null);
    const { setAccess, setExp, setUsername } = useAuth();
    const router = useRouter();

    async function logOut() {
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/auth/logout`,
                {
                    credentials: "include",
                }
            );
            const res = await response.json().catch(() => {});
            if (response.ok) {
                setAccess(undefined);
                setExp(undefined);
                setUsername(undefined);
                router.push("/");
            } else {
                console.log("error in backend");
                console.log(res.message);
            }
        } catch (err) {
            console.log("error occured in logout");
            console.log(err);
        }
    }

    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (
                panelRef.current?.contains(e.target as Node) ||
                buttonRef.current?.contains(e.target as Node)
            )
                return;
            setPanelOn(false);
        }

        window.addEventListener("click", handleClick, true);
        return () => window.removeEventListener("click", handleClick, true);
    }, []);

    return (
        <nav className="absolute top-0 left-0 right-0 z-50 flex flex-row justify-between items-center px-8 md:px-15 py-8">
            <div>
                <Link href="/">
                    <Image
                        src="/Logo.png"
                        alt="UWPLANNER logo"
                        width={1722}
                        height={1722}
                        className="h-10 w-auto"
                    />
                </Link>
            </div>
            <div className="flex flex-row justify-center gap-2 xs:gap-4 items-center">
                {signedIn ? (
                    <>
                        <div>
                            <Link href="/test" className="text-[1.2rem]">
                                Discussions
                            </Link>
                        </div>
                        <div>
                            <Link href="/test" className="text-[1.2rem]">
                                Courses
                            </Link>
                        </div>
                        <div>
                            <Link href="/test" className="text-[1.2rem]">
                                Graph
                            </Link>
                        </div>
                        <div>
                            <Link href="/test" className="text-[1.2rem]">
                                Semester
                            </Link>
                        </div>
                    </>
                ) : (
                    <>
                        <div>
                            <Link href="/login" className="text-[1.2rem]">
                                login
                            </Link>
                        </div>
                        <div className="hidden xs:block h-2 w-2 bg-dark-green rounded"></div>
                        <Link
                            href="/signUp"
                            className="px-5 xs:px-10 border-2 py-1 border-dark-green hover:text-light-green cursor-pointer relative overflow-hidden transition-all duration-700 text-center active:duration-500 active:bg-[#1a393d] active:border-[#1a393d] before:content-[''] before:absolute before:bg-dark-green before:transition-all before:duration-700 before:w-[200%] before:h-[200%] before:top-[110%] before:left-[110%]  hover:before:top-[-30px] hover:before:left-[-30px] before:z-[-1] before:rounded"
                        >
                            Sign Up
                        </Link>
                    </>
                )}

                <div className="relative">
                    <div
                        ref={buttonRef}
                        onClick={() => setPanelOn(signedIn && !panelOn)}
                        className="cursor-pointer"
                    >
                        <MdAccountCircle
                            style={{ height: "2.4rem", width: "auto" }}
                        />
                    </div>
                    {signedIn ? (
                        <div
                            ref={panelRef}
                            className={`absolute backdrop-blur-xs bg-[#4bac7f49] top-full px-3 rounded-lg right-1/2 translate-x-1/2 font-medium overflow-y-clip ${
                                panelOn ? "max-h-30 py-[0.85rem]" : "max-h-0"
                            } transition-all duration-500`}
                        >
                            {/* <div className="group relative w-fit">
                                <p className="max-w-[100px] truncate w-fit">
                                    {username}
                                </p>
                                <div className="absolute max-h-0 py-0 group-hover:max-h-6 transition-all duration-600 bg-slate-900/70 overflow-y-hidden text-green-100 text-xs px-2 group-hover:py-1 rounded-md top-5 -right-2">
                                    {username}
                                </div>
                            </div> */}
                            <HoverEffect text={username || ""}/>
                            <Link
                                href="/test"
                                className="items-center flex hover:text-[#1a3337] transition-colors duration-300"
                            >
                                <IoMdSettings className="mr-1" />
                                Settings
                            </Link>
                            <button
                                onClick={logOut}
                                className="mt-5 text-red-500 cursor-pointer flex items-center hover:text-red-700 transition-colors duration-300"
                            >
                                <MdExitToApp className="mr-1" />
                                Log Out
                            </button>
                        </div>
                    ) : (
                        ""
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

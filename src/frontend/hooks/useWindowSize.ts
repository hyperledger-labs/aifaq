import { useState } from 'react';
import { useDebounceCallback } from './useDebounceCallback';
import { useEventListener } from './useEventListener';
import { useIsomorphicLayoutEffect } from './useIsomorphicLayoutEffect';

type WindowSize<T extends number | undefined = number | undefined> = {
    width: T
    height: T
}

type UseWindowSizeOptions<InitializeWithValue extends boolean | undefined> = {
    initializeWithValue: InitializeWithValue
    debounceDelay?: number
}

const IS_SERVER = typeof window === 'undefined'

export function useWindowSize(options: UseWindowSizeOptions<false>): {
    windowSize: WindowSize,
    isMobile: boolean,
    isDesktop: boolean
}
export function useWindowSize(
    options?: Partial<UseWindowSizeOptions<true>>,
): {
    windowSize: WindowSize<number>,
    isMobile: boolean,
    isDesktop: boolean
}
export function useWindowSize(
    options: Partial<UseWindowSizeOptions<boolean>> = {},
): {
    windowSize: WindowSize | WindowSize<number>,
    isMobile: boolean,
    isDesktop: boolean
} {
    let { initializeWithValue = true } = options
    if (IS_SERVER) {
        initializeWithValue = false
    }

    const [windowSize, setWindowSize] = useState<WindowSize>(() => {
        if (initializeWithValue) {
            return {
                width: window.innerWidth,
                height: window.innerHeight,
            }
        }
        return {
            width: undefined,
            height: undefined,
        }
    })

    const debouncedSetWindowSize = useDebounceCallback(
        setWindowSize,
        options.debounceDelay,
    )

    function handleSize() {
        const setSize = options.debounceDelay
            ? debouncedSetWindowSize
            : setWindowSize

        setSize({
            width: window.innerWidth,
            height: window.innerHeight,
        })
    }

    useEventListener('resize', handleSize)

    useIsomorphicLayoutEffect(() => {
        handleSize()
    }, [])

    return {
        windowSize,
        isMobile: typeof windowSize.width === "number" && windowSize.width < 768,
        isDesktop:
            typeof windowSize.width === "number" && windowSize.width >= 768,
    }
}
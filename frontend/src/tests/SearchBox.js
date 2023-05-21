import {mount} from '@vue/test-utils'
import SearchBox from '../components/SearchBox.vue'

test('SearchBox component', async () => {
    expect(SearchBox).toBeTruthy()

    const mockRoute = {
        params: {
            query: 'urltest',
        }
    }

    const mockRouter = {
        push: vi.fn(),
    }

    const wrapper = mount(SearchBox, {
        props: {},
        global: {
            mocks: {
                $route: mockRoute,
                $router: mockRouter,
            }
        },
        attachTo: document.body,
    })

    await wrapper.get('button').trigger('click')

    expect(mockRouter.push).toHaveBeenCalledWith('/search/urltest')

    mockRouter.push.mockClear()

    await wrapper.find({ref: 'search-text'}).setValue('test2')

    await wrapper.get('button').trigger('click')

    expect(mockRouter.push).toHaveBeenCalledWith('/search/test2')

    mockRouter.push.mockClear()

    await wrapper.find({ref: 'search-text'}).setValue('äöüß!§$%&/()=?')

    await wrapper.get('button').trigger('click')

    expect(mockRouter.push).toHaveBeenCalledWith('/search/%C3%A4%C3%B6%C3%BC%C3%9F!%C2%A7%24%25%26%2F()%3D%3F')

    mockRouter.push.mockClear()

    await wrapper.find({ref: 'search-text'}).setValue('')

    await wrapper.get('button').trigger('click')

    expect(mockRouter.push).not.toHaveBeenCalled()

    expect(await wrapper.find({ref: 'search-text'}).element).toEqual(document.activeElement)

    expect(wrapper.html()).toMatchSnapshot()
})

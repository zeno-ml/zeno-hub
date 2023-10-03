import { env } from '$env/dynamic/private';
import {
	AuthenticationDetails,
	CognitoRefreshToken,
	CognitoUser,
	CognitoUserAttribute,
	CognitoUserPool,
	type CognitoUserSession,
	type ISignUpResult
} from 'amazon-cognito-identity-js';
import type { AuthUser } from './types';

export type CognitoUserSessionType = CognitoUserSession;

function getPool() {
	const CONFIGS = {
		UserPoolId: env.ZENO_USER_POOL_ID ?? '',
		ClientId: env.ZENO_USER_POOL_CLIENT_ID ?? ''
	};
	return new CognitoUserPool(CONFIGS);
}

/**
 * Login to Cognito User Pool using the provided credentials.
 * This will return the session data at the time of login.
 *
 * @param Username - Email address of the user to login
 * @param Password - Password of the user to login
 * @returns - Promise with the result of the login
 */
export const getSession = (Username: string, Password: string): Promise<CognitoUserSession> => {
	return new Promise((resolve, reject) => {
		const user = new CognitoUser({ Username, Pool: getPool() });
		user.authenticateUser(new AuthenticationDetails({ Username, Password }), {
			onSuccess: resolve,
			onFailure: reject
		});
	});
};

export function verify(Username: string, code: string) {
	const user = new CognitoUser({ Username, Pool: getPool() });
	return new Promise((resolve, reject) => {
		user.confirmRegistration(code, false, function (err, result) {
			if (err) reject(err);
			else resolve(result);
		});
	});
}

export const resendCode = (Username: string) => {
	const user = new CognitoUser({ Username, Pool: getPool() });
	user.resendConfirmationCode(() => {
		// Do nothing
	});
};

/**
 * Refresh the access token of the provided user.
 *
 * @param sessionData - Session data of the user with the refresh token
 * @returns - Promise with the new user object with tokens and expiration date
 */
export const refreshAccessToken = async (refreshToken: string): Promise<CognitoUserSession> => {
	const cognitoUser = getPool().getCurrentUser();
	// Check if the user is logged in
	if (!cognitoUser) {
		throw new Error('No user found');
	}
	// Refresh the session
	const RefreshToken = new CognitoRefreshToken({
		RefreshToken: refreshToken
	});
	return new Promise<CognitoUserSession>((resolve) => {
		cognitoUser.refreshSession(RefreshToken, (_resp, session: CognitoUserSession) => {
			resolve(session);
		});
	});
};

export async function signUpUserWithEmail(
	username: string,
	email: string,
	password: string
): Promise<ISignUpResult | undefined> {
	return new Promise(function (resolve, reject) {
		const attributeList = [
			new CognitoUserAttribute({
				Name: 'email',
				Value: email
			})
		];

		getPool().signUp(username, password, attributeList, [], function (err, res) {
			if (err) {
				reject(err);
			} else {
				resolve(res);
			}
		});
	});
}

export async function resetPassword(
	username: string,
	validation: string,
	password: string
): Promise<unknown> {
	return new Promise(function (resolve, reject) {
		const user = new CognitoUser({ Username: username, Pool: getPool() });
		user.confirmPassword(validation, password, {
			onSuccess: resolve,
			onFailure: reject
		});
	});
}

export async function sendPasswordResetCode(username: string) {
	const user = new CognitoUser({ Username: username, Pool: getPool() });
	user.forgotPassword({
		onSuccess: () => {
			// Do nothing
		},
		onFailure: () => {
			// Do nothing
		}
	});
}

export const extractUserFromSession = (session: CognitoUserSessionType): AuthUser => {
	if (!session?.isValid?.()) throw new Error('Invalid session');
	const user = session.getIdToken().payload;
	return {
		id: user.sub,
		name: user['cognito:username'],
		email: user.email,
		image: user.picture,
		accessToken: session.getAccessToken().getJwtToken(),
		accessTokenExpires: session.getAccessToken().getExpiration(),
		refreshToken: session.getRefreshToken().getToken()
	};
};
